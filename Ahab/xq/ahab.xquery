xquery version "3.0";

(:
 : This file is a try for porting MarkLogic and BaseX implementation of maps
 : 
 : Thibault Clérice
 : ponteineptique@github
 :)

module namespace ahabx = "http://github.com/capitains/ahab/x";

import module namespace kwic="http://exist-db.org/xquery/kwic";
declare namespace ahab = "http://github.com/capitains/ahab";
declare namespace CTS = "http://chs.harvard.edu/xmlns/cts";
declare namespace ti = "http://chs.harvard.edu/xmlns/cts";
declare namespace util="http://exist-db.org/xquery/util";
declare namespace ft="http://exist-db.org/xquery/lucene";
declare namespace tei="http://www.tei-c.org/ns/1.0";



(: 
 : Get the xpath of the smallest node for a given text record.
:)
declare function ahabx:smallestCitationNode($a_text_record) {
    let $citation := ($a_text_record//ti:citation)[last()]
    
    let $first := replace(fn:string($citation/@scope), "\]", " and @type]")
    let $last := fn:string($citation/@xpath)
    
    let $scope := fn:concat($first, $last)
    let $xpath := replace($scope,"='\?'",'')
    return $xpath
};

(: 
 :)
declare function ahabx:collectionFromUrn($a_urn) {
    let $components := fn:tokenize($a_urn, ":")
    let $namespace := $components[3]
    let $workComponents := fn:tokenize($components[4], "\.")
    let $path := ($namespace, $workComponents)
    return fn:string-join($path, "/")
};

(: 
 : $a_urn Urn or namespace
 : $a_query Query
 :)
declare function ahabx:search($a_urn, $a_query, $a_start, $a_limit)
{
    let $collection_from_urn := ahabx:collectionFromUrn($a_urn)
    let $collection := fn:concat("/db/repository/", $collection_from_urn)
    let $config := <config xmlns="" width="60"/>
    let $hits := collection($collection)//tei:body[ft:query(., $a_query)]
    
    let $matches := for $hit in $hits return kwic:expand($hit)
    let $hitCount :=  count($matches//exist:match)
    
    let $results := for $hit in $hits
        let $path := fn:concat(util:collection-name($hit), "/", util:document-name($hit))
        let $docname := collection("/db/repository/inventory")//ti:online[@docname=$path] 
        let $editionNode := $docname/..
        
        let $urn := if ($editionNode/@urn)
            then fn:string($editionNode/@urn)
        else
            let $edition := tokenize($docname/../@projid, ":")[2]
            let $work := tokenize($docname/../../@projid, ":")[2]
            let $textgroup := tokenize($docname/../../../@projid, ":")[2]
            
            return concat("urn:cts:",$textgroup,".",$work,".",$edition)
            
        let $expanded := kwic:expand($hit)
        
        let $xpath := replace(ahabx:smallestCitationNode($docname/..), "//", "/   /")
        let $tokenizedPath := tokenize($xpath, "/")
        
        let $indexOfBody := if(index-of($tokenizedPath, "tei:body"))
            then index-of($tokenizedPath, "tei:body")
            else index-of($tokenizedPath, "body")
        
        let $subsequence := subsequence($tokenizedPath, $indexOfBody + 1, count($tokenizedPath) - $indexOfBody)
        let $joinedXpath := fn:string-join($subsequence, "/")
        let $reduced_xpath := replace($joinedXpath, "   ", "")
        let $lastChar := substring($reduced_xpath, string-length($reduced_xpath), 1)
        let $eval := if($lastChar = "]")
        then fn:concat("$expanded/", substring($reduced_xpath, 1, string-length($reduced_xpath) - 1), " and .//exist:match]")
        else fn:concat("$expanded/", $reduced_xpath, "node()[.//exist:match]") 
        let $contexts := util:eval($eval)
        
        return for $context in $contexts
            let $passage := for $citation in $docname//ti:citation
                let $label := fn:lower-case(fn:string($citation/@label))
                return if (fn:string($citation/@xpath) = "//tei:l[@n='?']" or fn:string($citation/@xpath) = "/tei:l[@n='?']") (: Dirty hack :)
                then fn:string($context/ancestor-or-self::node()[@n][1]/@n)
                else fn:string($context/ancestor-or-self::node()[@n and fn:lower-case(@type)=$label][1]/@n)
                
            let $passage_urn := fn:concat($urn, ":", fn:string-join($passage, "."))
            
            return for $context_match in $context//exist:match
                return 
                    element ahab:result {
                        element ahab:urn { $urn },
                        element ahab:passageUrn { $passage_urn },
                        element ahab:text { kwic:get-summary($context, $context_match, $config) }
                    }
    return 
        element ahab:reply {
            element ahab:query   { $a_query },
            element ahab:urn     { $a_urn },
            element ahab:results { 
                attribute ahab:start { $a_start },
                attribute ahab:limit { $a_limit },
                attribute ahab:count { $hitCount },
                for $res in subsequence($results, $a_start, $a_limit) return $res 
            }
        }
};

(: 
 : $a_urn Urn or namespace
 : $a_query Query
 :)
declare function ahabx:permalink($a_urn)
{
    let $parsed_urn := ahabx:simpleUrnParser($a_urn)
    let $work := collection("/db/repository/inventory")//ti:work[@urn = $parsed_urn/workUrn/text()]
    let $inv := $work/ancestor::*[@tiid][1]/@tiid
    
    let $urn := 
        if (fn:empty($parsed_urn/version/text()))
        then fn:string($work/ti:edition[1][@urn]/@urn)
        else fn:string($parsed_urn/version/text())
        
    let $urn_passage :=
        if (fn:empty($parsed_urn/passage/text()))
        then $urn
        else $urn || ":" || fn:string($parsed_urn/passage/text())
        
    let $request :=
        if (fn:empty($parsed_urn/passage/text()))
        then "GetValidReff"
        else "GetPassagePlus"
        
    return element ahab:reply {
        element ahab:urn { $urn_passage },
        element ahab:request { fn:string($request) },
        element ahab:inventory { fn:string($inv) }
    }
};

declare function ahabx:simpleUrnParser($a_urn)
{
    let $components := fn:tokenize($a_urn, ":")
    let $namespace := $components[3]
    let $workComponents := fn:tokenize($components[4], "\.")
    (: TODO do we need to handle the possibility of a work without a text group? :)
    let $textgroup := $workComponents[1]
    let $work := $workComponents[2]

    let $passage := $components[5]
    let $passageComponents := fn:tokenize($components[5], "-")
    let $part1 := $passageComponents[1]
    let $part2 := $passageComponents[2]
    let $part2 := if (fn:empty($part2)) then $part1 else $part2

    let $namespaceUrn := fn:string-join($components[1,2,3], ":")
    let $groupUrn := if (fn:exists($textgroup)) then $namespaceUrn || ":" || $textgroup else ()
    let $workUrn := if(fn:exists($work)) then $groupUrn || "." || $work else ()
    let $version := if(fn:exists($workComponents[3])) then $workUrn || "." || $workComponents[3] else ()
    
    
    return
      element reply
      {
        element urn { $a_urn },
        (: urn without any passage specifics:)
        element groupUrn { $groupUrn },
        element workUrn { $workUrn },
        element namespace{ $namespaceUrn },
        element version { $version },
        element passage { $passage }
      }
};
