# -*- coding: utf-8 -*-

treebank = {
    "endpoint.create" : "http://sosol.perseids.org/sosol/dmm_api/create/item/TreebankCite/DOC_REPLACE",
    "endpoint.create.linked_urn" : "http://sosol.perseids.org/sosol/cite_publications/create_from_linked_urn/Treebank/COLLECTION_REPLACE?init_value[]=URL_REPLACE",

    "tokenization.endpoint" : "http://services2.perseids.org/llt/segtok",
    "tokenization.params" : "xml inline split-tokens|splitting merge-tokens|merging shift-tokens|shifting inputtext|text remove_node[] go_to_root ns",
    "tokenization.xslt" : "/apps/static/xslt/segtok_to_tb.xsl",

    "oa.xslt" : "/apps/static/xslt/wrap_treebank.xsl",

    "editor.url" : "http://www.perseids.org/tools/arethusa/app/#/perseids",
    "workListUrl" : "http://sosol.perseids.org/exist/rest/db/xq/ctsworklist.xq?inv=annotsrc"
}
