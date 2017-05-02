module.exports = {
    "env": {
        "browser": true,
        "commonjs": true,
        "es6": true,
        "node": true
    },
    "extends": ["plugin:requirejs/recommended", "eslint:recommended"],
    "rules": {
        "indent": [
            "error",
            4
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "error",
            "double"
        ],
        "semi": [
            "error",
            "always"
        ],
	"jsdoc/check-param-names": 1,
        "jsdoc/check-tag-names": 1,
        "jsdoc/check-types": 1,
        "jsdoc/newline-after-description": 1,
        "jsdoc/require-description-complete-sentence": 1,
        "jsdoc/require-hyphen-before-param-description": 1,
        "jsdoc/require-param": 1,
        "jsdoc/require-param-description": 1,
        "jsdoc/require-param-type": 1,
        "jsdoc/require-returns-description": 1,
        "jsdoc/require-returns-type": 1,
	    "requirejs/no-invalid-define": 2,
        "requirejs/no-multiple-define": 2,
        "requirejs/no-named-define": 2,
        "requirejs/no-commonjs-wrapper": 2,
        "requirejs/no-object-define": 1,
	"requirejs/amd-function-arity": [2, { "allowExtraDependencies": true }]
    },
   "plugins": ["requirejs", "jsdoc"]
};
