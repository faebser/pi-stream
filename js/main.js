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
			var icon = 'icon-cross_mark'
			if(object.status === 'attention') icon = 'icon-information_white';
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
	piStream.init();
})