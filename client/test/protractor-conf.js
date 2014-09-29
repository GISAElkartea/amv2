exports.config = {
    allScriptsTimeout: 11000,
    specs: [
        'e2e/**/*.js'
    ],

    multiCapabilities: [/*{
    'browserName': 'firefox'
    }, */{
    'browserName': 'chrome'
    }],

    baseUrl: 'http://localhost:3333/',

    framework: 'jasmine',

    jasmineNodeOpts: {
        defaultTimeoutInterval: 60000
    }
};
