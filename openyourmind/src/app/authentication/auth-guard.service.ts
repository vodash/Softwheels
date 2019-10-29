import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { AuthService } from './authService';
import {Router} from '@angular/router';

@Injectable()

export class AuthGuardService implements CanActivate {
    constructor(public AuthServices: AuthService, public reRouter: Router) {
    }
    canActivate() {
        if ( this.AuthServices.isLoggedIn()) {
            return true;
        } else {
            window.alert('You do not have permission to view this page. Try logging in');
            this.reRouter.navigate(['/']);
            return false;
        }
    }
}
