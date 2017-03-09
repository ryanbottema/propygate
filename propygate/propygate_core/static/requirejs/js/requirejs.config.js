
require.config({
    //urlArgs: 'v=' + siteConfig.VERSION,
    urlArgs: (function () {
        if (siteConfig.DEBUG == 'True')
            return 'v=' + Math.random();
        return 'v=' + siteConfig.VERSION;
    }()),
    baseUrl: siteConfig.STATIC_URL,
    paths: {
        // Third party:
        adminlte: siteConfig.STATIC_URL + 'adminlte/js/app.min',
        adminlte_config: siteConfig.STATIC_URL + 'adminlte/js/adminlte.config',
        bootstrap: siteConfig.STATIC_URL + 'bootstrap/js/bootstrap.min',
        d3: siteConfig.STATIC_URL + 'd3/js/d3',
        //daterangepicker: siteConfig.STATIC_URL + 'daterangepicker/js/daterangepicker',
        //datatables: siteConfig.STATIC_URL + 'listable/js/jquery.dataTables.min',
        //'datatables.bootstrap': siteConfig.STATIC_URL + 'listable/js/jquery.dataTables.bootstrap',
        //'datatables.columnFilter': siteConfig.STATIC_URL + 'listable/js/jquery.dataTables.columnFilter',
        //'datatables.searchPlugins': siteConfig.STATIC_URL + 'listable/js/jquery.dataTables.searchPlugins',
        //'datatables.sort': siteConfig.STATIC_URL + 'listable/js/jquery.dataTables.sort',
        //datepicker: siteConfig.STATIC_URL + 'datepicker/js/bootstrap-datepicker.min',
        jquery: siteConfig.STATIC_URL + 'jquery/js/jquery-3.1.1.min',
        //listable: siteConfig.STATIC_URL + 'listable/js/listable',
        //lodash: siteConfig.STATIC_URL + 'lodash/js/lodash.min',
        //multiselect: siteConfig.STATIC_URL + 'multiselect/js/bootstrap.multiselect',
        moment: siteConfig.STATIC_URL + 'moment/js/moment.min',
        //select2: siteConfig.STATIC_URL + 'select2/js/select2.min',
        slimscroll: siteConfig.STATIC_URL + 'slimscroll/js/jquery.slimscroll.min',

        // Site wide:
        base: siteConfig.STATIC_URL + 'propygate_core/js/base',
        home: siteConfig.STATIC_URL + 'propygate_core/js/home'
        
    },
    shim: {
        adminlte: {
            deps: ['jquery', 'bootstrap', 'slimscroll', 'adminlte_config']
        },
        bootstrap: {
            deps: ['jquery']
        },
        jquery: {
            exports: '$'
        },
        base: {
            deps: ['jquery', 'adminlte']
        },
        slimscroll: {
            deps: ['jquery']
        },
    }
});