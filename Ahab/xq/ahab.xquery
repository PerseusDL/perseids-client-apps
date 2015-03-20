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
declare function ahabx:search($a_urn, $a_query)
{
    let $collection_from_urn := ahabx:collectionFromUrn($a_urn)
    let $collection := fn:concat("/db/repository/", $collection_from_urn)
    let $config := <config xmlns="" width="60"/>
    let $results := for $hit in collection($collection)//tei:body[ft:query(., $a_query)]
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
                return <result>
                        <urn>{$urn}</urn>
                        <passage>{$passage_urn}</passage>
                        <text>{kwic:get-summary($context, $context_match, $config)}</text>
                    </result>
    return <reply>
            <query>{$a_query}</query>
            <collection>{$a_urn}</collection>
            <results>{$results}</results>
        </reply>
};
