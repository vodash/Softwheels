import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { AuthService } from './authService';
import {Router} from '@angular/router';

@Injectable()

export class LoginAuthGuardService implements CanActivate {
    constructor(public AuthServices: AuthService, public reRouter: Router) {
    }
    // This function checks is the user is logged in. If this is true they will be redirected from the login page
    canActivate() {
        if ( this.AuthServices.isLoggedIn()) {
            this.reRouter.navigateByUrl('/profile')
            return false;
        } else {
            return true;
        }
    }
}
