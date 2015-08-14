// build a store that connets the state to the backend
var backendStore = (function ($, Vue, superagent) {
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

		console.log(item.status === 'attention');

		if(item.status === 'attention') { 
			icon = icons.info;
			title = 'Warning';
		}

		console.log(icon);
		return {
			'class': item.status,
			'icon': icon,
			'message': item.message,
			'title': title
		}
	};
	// public methods
	module.init = function () {
		module.getStatus();
	},
	module.getStatus = function () {
		var self = this;
		superagent.get(urls.status)
			.end(function (error, response) {
				module.statusList = response.body.filter(statusListFilter).map(statusListMap);
				module.hasStatusItems = module.statusList.length !== 0;
				console.log(module.statusList);
				console.log(module.hasStatusItems);
			});
	};
	//return the module
	return module;
}(jQuery, Vue, superagent));

// build two components
// build a function that returns an intial state (global vars are not fun, but in this case its like a user session)
// use the module pattern for the state

var stateFactory = (function ($, backendStore) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var initalState = {
		'isStreaming': false,
		'isValidForm': false,
		'errorList': [],
		'formData': {
			name: {
				value: '',
				valid: simpleValidator
			},
			description: {
				value: '',
				valid: simpleValidator
			},
			url: {
				value: 'nonoradio.tumblr.com',
				valid: simpleUrlValidator
			},
			genre: {
				value: '',
				valid: function () {
					return true;
				}
			}
		},
		'store': {}
	},
	module = {};
	// private methods
	var simpleValidator = function () {
		if(this.value != '') return true;
		return false;
	},
	simpleUrlValidator = function () {
		var aElement;
		if(this.value.indexOf('http://') !== 1 || this.value.indexOf('https://') !== 1) {
			aElement = $('<a />').attr('href', 'http://' + this.value);
		}
		else {
			aElement = $('<a />').attr('href', this.value);
		}

		console.log(aElement.hostname);

		return Boolean(aElement.hostname);
	};
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
				},
				getStatus: function () {
					
				}
			},
			created: function () {
				console.log('i raise master');
				
			}
		});

		var streamFormComponent = Vue.extend({
			'data': {
				state: state
			},
			'template': $('#streamFormTemplate').html(),
			created: function () {
				console.log('i raise too, master!');
			}
		});

		var streamButtonComponent = Vue.extend({
			'data': {
				state: state
			},
			template: $('#streamButtonTemplate').html(),
			created: function () {
				console.log('the button raises to be clicked!');
			}
		});

		var testButtonComponent = Vue.extend({
			data: {
				state: state
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


var piStream = (function ($, Vue, superagent) {
	// javascript module pattern
	"use strict"; // enable strict mode for javascript module
	// private vars
	var module = {},
		status = null,
		errorList = null,
		bigButton = null,
		streamForm = null,
		urls = {
			'status': '/status',
			'tests': '/run-tests',
			'stream': '/stream'
		};
	// private methods
	var errorMap = function(object) {
		if(object && object.status && object.status !== 'good') {
			var icon = 'icon-cross_mark';
			var message = '<span>Error:</span>' + object.message;

			if(object.status === 'attention') {
				icon = 'icon-information_white';
				message = '<span>Warning:</span>' + object.message;
			} 
			return {
				'class': object.status,
				'icon': icon,
				'message': object.message
			}
		}
	},
	runStream = function (callback) {
		// validate form - nope
		// submit form
		var isFormValid = true;
		for (var i in streamForm.$data) {
			var e = streamForm.$data[i];

			if(e) {
				if(e.valid() === false) {
					isFormValid = false;
					e.class = "invalid";
				}
				else {
					e.class = 'valid';
				}
			}

		};

		if(isFormValid) {
			superagent.post(urls.stream)
				.set('Content-Type', 'application/json')
				.send(streamForm.$data)
				.end(function(error, response) {
					console.log(error);
					console.log(response);
				});

			window.setTimeout(function() {
				superagent.get(urls.stream).end(function(response){
					console.log(response);
					var status = response.body;
					if(status.errors == 0) {
						bigButton.title = 'Darkice is running';
						streamForm.formClass = 'hidden';
						errorList.items.push({
							'class': 'attention',
							'icon': 'icon-information_white',
							'message': 'Streaming-Link: ' + status.link
						});
					}
					else {
						errorList.items = response.body.messages.map(errorMap).filter(Boolean);
					}
				})
			}, 5000)
		}
		else {
			bigButton.class = 'bad';
			bigButton.title = 'Please fix the form';
			bigButton.action = 'stream';
			bigButton.spanClass = 'hidden';
			bigButton.spanText = '';
			window.setTimeout(function() {
				updateButton();
			}, 5000);
		}
	},
	runTests = function (callback) {
		// rerun test
		// update the list
		// update buttons
		superagent.get(urls.tests).end(function(response) {
			status = response.body;
			errorList.items = status.map(errorMap).filter(Boolean);
			updateButton();
			if(callback) callback();
		});
	},
	updateButton = function () {
		if (errorList.hasErrors) {
			bigButton.class = 'bad';
			bigButton.title = 'rerun tests';
			bigButton.action = 'tests';
			bigButton.spanText = '';
			bigButton.spanClass = 'hidden';
		}
		else {
			bigButton.class = 'good';
			bigButton.title = 'stream';
			bigButton.action = 'stream';
			bigButton.spanClass = 'hidden';
			bigButton.spanText = '';
		}
	};
	// public methods
	module.init = function () {
		superagent.get(urls.status).end(function(response){
	   		status = response.body;

		   	errorList = new Vue({
				'el': '.errorList',
				'data': {
					'items': status.map(errorMap).filter(Boolean)
				},
				'computed': {
					'hasErrors': function() {
						for(var i = 0; i < this.items.length; i++) {
							if(this.items[i].class == 'error') return true;
						}
						return false;
					}
				}
			});

			console.log(errorList.items);
			var errors = errorList.hasErrors;

			var buttonData = {
				'class': 'good',
				'action': 'stream',
				'spanClass': 'hidden',
				'spanText': '',
				'title': 'stream'
			};

			if(errors) {
				buttonData.class = 'bad';
				buttonData.title = 'rerun tests';
				buttonData.action = 'tests';
			}

			bigButton = new Vue({
				'el': '.buttons a',
				'data': buttonData,
				'methods': {
					'buttonTrigger': function(e) {
						if(this.action === 'stream') {
							this.title = 'starting darkice'
							this.spanClass = 'loading';
							this.spanText = 'starting darkice';
							runStream();
						}
						else if(this.action === 'tests') {
							this.title = 'running tests'
							this.spanClass = 'gauge';
							this.spanText = 'runnig tests'; 
							runTests();
						}
					}
				}
			});

			streamForm = new Vue({
				'el': '#streamForm',
				'data': {
					'formClass': '',
					'name': {
						'value': '',
						'valid': function() {
							if(this.value != '') return true;
							return false;
						},
						'class': ''
					},
					'description': {
						'value': '',
						'valid': function() {
							if(this.value != '') return true;
							return false;
						},
						'class': ''
					},
					'url': {
						'value': 'http://nonoradio.tumblr.com',
						'valid': function() {
							if(this.value != '') return true;
							return false;
						},
						class: ''
					},
					'genre': {
						'value': '',
						'valid': function() {
							return true;
						},
						'class': ''
					},
				}
			})
			console.log(streamForm);
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