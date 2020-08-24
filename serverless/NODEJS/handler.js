'use strict';
const funcDev = require('./handlerDev');
const funcProd = require('./handlerProd');

module.exports.main = (event, context, callback) => {

	let response;

	if(event.env.includes('localhost')){
		switch(event.func) {
			case 'signUp':
				response = funcDev.signUp(event, context, callback);
				break;
			case 'confirmCode':
				response = funcDev.confirmCode(event, context, callback);
				break;
			case 'signIn':
				response = funcDev.signIn(event, context, callback);
				break;
			case 'updateUser':
				response = funcDev.updateUser(event, context, callback);
				break;
			case 'deleteUser':
				response = funcDev.deleteUser(event, context, callback);
				break;
			case 'resetPassword':
				response = funcDev.resetPassword(event, context, callback);
				break;
			case 'checkUser':
				response = funcDev.checkUser(event, context, callback);
				break;
			case 'confirmPassword':
				response = funcDev.confirmPassword(event, context, callback);
				break;
			case 'confirmMFA':
				response = funcDev.confirmMFA(event, context, callback);
				break;
		}
	} else {
		switch(event.func) {
			case 'signUp':
				response = funcProd.signUp(event, context, callback);
				break;
			case 'confirmCode':
				response = funcProd.confirmCode(event, context, callback);
				break;
			case 'signIn':
				response = funcProd.signIn(event, context, callback);
				break;
			case 'updateUser':
				response = funcProd.updateUser(event, context, callback);
				break;
			case 'deleteUser':
				response = funcProd.deleteUser(event, context, callback);
				break;
			case 'resetPassword':
				response = funcProd.resetPassword(event, context, callback);
				break;
			case 'checkUser':
				response = funcProd.checkUser(event, context, callback);
				break;
			case 'confirmPassword':
				response = funcProd.confirmPassword(event, context, callback);
				break;
			case 'confirmMFA':
				response = funcProd.confirmMFA(event, context, callback);
				break;
		}
	}
	
	return response;
};