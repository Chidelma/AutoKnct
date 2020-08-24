const AmazonCognitoIdentity = require('amazon-cognito-identity-js');
global.fetch = require('node-fetch');
const Amplify = require('aws-amplify');
const nodemailer = require('nodemailer');
const Auth = Amplify.Auth;

Amplify.default.configure({ 
	Auth : {
		identityPoolId: 'us-east-1:e5b74544-35ff-4c24-9a62-59c07a7db5a8',
		region: 'ca-central-1',
		identityPoolRegion: 'us-east-1',
		userPoolId: 'ca-central-1_YslZwdQdK',
		userPoolWebClientId: 'hhj39244ktpq30gbq9ut6b84p'
	}
});

let cognitoUser = null;

const poolData = {    
    UserPoolId : 'ca-central-1_YslZwdQdK', // Your user pool id here    
    ClientId : "hhj39244ktpq30gbq9ut6b84p" // Your client id here
}; 

const pool_region = 'ca-central-1';

const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

exports.signIn = (event,context,callback) => {

	Auth.signIn(event.username, event.password).then(user => {

		if(user.challengeName === 'SOFTWARE_TOKEN_MFA' && event.code != '') {
			Auth.confirmSignIn(user, event.code, 'SOFTWARE_TOKEN_MFA').then(loggedUser => {
				callback(null, loggedUser.signInUserSession);
			}).catch(err => {
				callback(err);
			});
		} else if(event.newPassword != '') {
			Auth.completeNewPassword(user, event.newPassword, user.challengeParam.requiredAttributes).then(() => {
				Auth.setupTOTP(user).then((code) => {
					callback(null, { key : code, tokns : user.signInUserSession });
				}).catch(err => {
					callback(err);
				});
			}).catch(err => {
				callback(err);
			});
		} else {
			callback(null, user.signInUserSession);
		}
		
	}).catch(err => {
		callback(err);
	});

}


exports.signUp = (event,context,callback) => {

	var attributeList = [];

	var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute({ Name: 'email', Value: event.email });
	var attributeName = new AmazonCognitoIdentity.CognitoUserAttribute({ Name: 'name', Value: event.name });

	attributeList.push(attributeEmail); attributeList.push(attributeName);

	userPool.signUp(event.username, event.password, attributeList, null, function(err, result) {
		callback(err, result);
	});
		
}


exports.confirmCode = (event,context,callback) => {

	if(event.resend) {

		Auth.resendSignUp(event.username).then(() => {
			callback(null, 'code resent successfully');
		}).catch(e => {
			callback(e);
		});

	} else {

		Auth.confirmSignUp(event.username, event.code, {
			forceAliasCreation: false
		}).then(data => callback(null, data))
		  .catch(err => callback(err));

	}

}

exports.updateUser = (event,context,callback) => {

	Auth.signIn(event.username, event.password).then(user => {

		Auth.updateUserAttributes(user, {
			'email': event.email,
			'name': event.name
		}).then(result => {
			callback(null, result);
		}).catch(e => {
			callback(e);
		});
		
	}).catch(err => {
		callback(err);
	});

}

exports.resetPassword = (event,context,callback) => {

	Auth.signIn(event.username, event.oldPassword).then(user => {
		return Auth.changePassword(user, event.oldPassword, event.newPassword);
	}).catch(err => {
		callback(err);
	});

}

exports.checkUser = (event,context,callback) => {

	Auth.forgotPassword(event.username)
    .then(data => callback(null, data))
    .catch(err => callback(err));
}

exports.confirmPassword = (event,context,callback) => {

	Auth.forgotPasswordSubmit(event.username, event.code, event.password)
	.then(data => callback(null, data))
	.catch(err => callback(err));
	
}

exports.confirmMFA = (event,context,callback) => {

	Auth.signIn(event.username, event.password).then(user => {
		Auth.verifyTotpToken(user, event.code).then(() => {
			Auth.setPreferredMFA(user, 'TOTP').then(data => {
				callback(null, data); 
			}).catch(err => {
				callback(err);
			});
		}).catch( e => {
			callback(e);
		});
	}).catch(err => {
		callback(err);
	});
	
}