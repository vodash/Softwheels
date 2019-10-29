import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map} from 'rxjs/operators';
import {environment} from '../../htpp-conf';
import {Router} from '@angular/router';

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    constructor(private http: HttpClient, public reRouter: Router) {
    }

    login(username: string, password: string ) {
        console.log(username, password);
        // TODO: make a redirect to another page one logged in
        return this.http.post(environment.adress + '/auth', {username, password}).pipe(map(user => {
            // store user details and jwt token in local storage to keep user logged in between page refreshess
            this.setStorage(user['access_token']);
        }));
    }

    setStorage(user: any) {
        localStorage.setItem('id_token', JSON.stringify(user));
    }

    logout() {
        localStorage.removeItem('id_token');
    }
    isLoggedIn(): boolean {
        if (localStorage.getItem('id_token')) {
            return true;
        } else {
            return false;
        }
    }
}

