﻿define(
    [
        'plugins/router',
        'durandal/app',
        'jquery',
        'knockout',
        'service',
        'model/loginModel',
        'model/adminModel',
        'model/environmentModel',
        'model/pillarModel',
        'model/toolsModel',
        'bootstrap'
    ],
    function(router, app, $, ko, service, login, admin, environment, pillar, tools) {
        return {
            router: router,
            login: login,
            admin: admin,
            environment: environment,
            pillar: pillar,
            tools: tools,
            isFAQ: function(title) {
                return title.search('FAQ') !== -1;
            },
            activate: function() {
                router.map([
                    { route: '', title: 'Application State', moduleId: 'viewmodels/applicationState', nav: true },
                    { route: 'config(/:server)', title: 'Server Config', moduleId: 'viewmodels/serverConfig', nav: true, hash: '#config' },
                    { route: 'pillar', title: 'Pillar Config', moduleId: 'viewmodels/pillarConfig', nav: true },
                    { route: 'tools', title: 'ZK Tools', moduleId: 'viewmodels/tools'},
                    { route: 'appFAQ', title: 'App State FAQ', moduleId: 'viewmodels/faq/applicationState', nav: true },
                    { route: 'configFAQ', title: 'Server Config FAQ', moduleId: 'viewmodels/faq/serverConfig', nav: true }
                ]).buildNavigationModel();

                return router.activate();
            }
        };
    });
