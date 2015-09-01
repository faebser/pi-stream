// build a store that connets the state to the backend
var backendStore = (function ($, Vue, superagent, Plite) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var urls = {
			'status': '/status',
			'tests': '/run-tests',
			'stream': '/stream'
	},
	icons = {
			error: 'icon-cross_mark',
			info: 'icon-information_white'
	},
	module = {
		statusList: [],
		hasStatusItems : false
	};
	// private methods
	var statusListFilter = function (item) {
		return item.status !== 'good';
	},
	statusListMap = function (item) {
		var icon = icons.error;
		var title = 'Error';

		if(item.status === 'attention') { 
			icon = icons.info;
			title = 'Warning';
		}

		return {
			'class': item.status,
			'icon': icon,
			'message': item.message,
			'title': title
		}
	},
	updateStatusList = function updateStatusList (response) {
		module.statusList = response.body.filter(statusListFilter).map(statusListMap);
		module.hasStatusItems = module.statusList.length !== 0;
	};
	// public methods
	module.init = function () {
		//module.getStatus();
	},
	module.getStatus = function () {
		var self = this;
		superagent.get(urls.status)
			.end(function (error, response) {
				if(!Boolean(error)) {
					updateStatusList(response);
				}
			});
	},
	module.sendStreamFormData = function (formData) {
		var serializedObject = JSON.stringify(formData);
		var promise = new Plite();

		superagent
			.post(urls.stream)
			.send(formData)
			.end(function (error, response) {
				if(error) {
					promise.reject(error);
				}
				else {
					promise.resolve(response);
				}
				console.log(error);
				console.log(response);
			});

		return promise;
	},
	module.rerunTests = function () {
		var promise = Plite();

		superagent
			.get(urls.tests)
			.end(function getResponse (error, response) {
				if(error) {
					promise.reject(error);
				}
				else {
					module.statusList = [];
					updateStatusList(response);
					promise.resolve();
				}

				console.log(error);
				console.log(response);
			});

		return promise;
	};
	//return the module
	return module;
}(jQuery, Vue, superagent, Plite));

// build two components
// build a function that returns an intial state (global vars are not fun, but in this case its like a user session)
// use the module pattern for the state

var stateFactory = (function ($, backendStore) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module

	// private methods
	var simpleValidator = function () {
		if(this.value != '') return true;
		return false;
	},
	toJSON = function () {
		return this.value;
	},
	makeAelementOutOfString = function (inputString) {
		var aElement;
		if(inputString.indexOf('http://') !== 1 || inputString.indexOf('https://') !== 1) {
			aElement = $('<a />').attr('href', 'http://' + inputString);
		}
		else {
			aElement = $('<a />').attr('href', inputString);
		}

		return aElement;
	},
	simpleUrlValidator = function () {
		var aElement = makeAelementOutOfString(this.value);
		return Boolean(aElement.get(0).hostname);
	};

	// private vars
	var initalState = {
		'isStreaming': false,
		'isValidForm': false,
		'errorList': [],
		'formData': {
			name: {
				value: '',
				validator: simpleValidator,
				isValid: false,
				toJSON: toJSON
			},
			description: {
				value: '',
				validator: simpleValidator,
				isValid: false,
				toJSON: toJSON
			},
			url: {
				value: 'nonoradio.tumblr.com',
				validator: simpleUrlValidator,
				isValid: false,
				toJSON: function () {
					return makeAelementOutOfString(this.value).get(0).href;
				}
			},
			genre: {
				value: '',
				validator: function () {
					return true;
				},
				isValid: true,
				toJSON: toJSON
			}
		},
		'store': {}
	},
	module = {};
	// public methods
	module.init = function (options) {
		backendStore.init();
		initalState.store = backendStore;
		return $.extend(initalState, options);
	};
	//return the module
	return module;
}(jQuery, backendStore));

var app = (function ($, Vue, superagent) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {};
	// private methods
	// public methods
	module.init = function () {
		var state = stateFactory.init();
		state.store.getStatus();
		// with this state, build the components
		// js pass by ref should be able to update the state inside the components

		var errorListComponent = Vue.extend({
			'data': {
				state: state
			},
			'template': $('#errorListTemplate').html(),
			methods: {
				clickTest: function () {
					this.state.urls.status = 'test3';
					console.log(state.urls.status);
				}
			},
			created: function () {
				console.log('i raise master');
			}
		});

		var streamFormComponent = Vue.extend({
			data: {
				state: state,
				timeout: -1
			},
			template: $('#streamFormTemplate').html(),
			methods: {
				testForm: function () {
					var self = this;
					// add timeout to check values after a while, ca 200 ms or else cancel timeout
					if (self.timeout !== -1) {
						window.clearTimeout(self.timeout);
					}
					this.timeout = window.setTimeout(function () {
						self.validateForm();
					}, 200);
				},
				validateForm: function validateForm () {
					_.forEach(state.formData, function validateForm (element) {
						element.isValid = element.validator();
					});
				}
			},
			created: function () {
				console.log('i raise too, master!');
				this.validateForm();
			}
		});

		var streamButtonComponent = Vue.extend({
			'data': {
				state: state
			},
			template: $('#streamButtonTemplate').html(),
			methods: {
				runStream: function () {
					this.state.store.sendStreamFormData(this.state.formData);
				}
			},
			created: function () {
				console.log('the button raises to be clicked!');
			}
		});

		var testButtonComponent = Vue.extend({
			data: {
				state: state
			},
			methods: {
				rerunTests: function () {
					var self = this;
					self.state.statusListLoading = true;
					self.state.store.rerunTests()
						.then(
							function success () {
								self.state.statusListLoading = false;
							},
							function error (error) {
								console.log(error);
							}
						);
				}
			},
			template: $('#testButtonTemplate').html()
		});

		Vue.component('error-list', errorListComponent);
		Vue.component('stream-form', streamFormComponent);
		Vue.component('stream-button', streamButtonComponent);
		Vue.component('test-button', testButtonComponent);

		var mainApp = new Vue({
			el: '#app',
			data: {
				'state': state
			},
			components: {
				'errorList': errorListComponent,
				'streamForm': streamFormComponent,
				'streamButton': streamButtonComponent,
				'testButton': testButtonComponent
			},
			methods: {

			},
			created: function () {
				console.log('main app init');
			}
		});
	};
	//return the module
	return module;
}(jQuery, Vue, superagent));


$(document).ready(function(){
	//piStream.init();
	app.init();
	$(document).scrollTop(0);
})