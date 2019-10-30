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
        return this.http.post(environment.adress + '/auth', {username, password}).pipe(map(user => {
            // store user details and jwt token in local storage to keep user logged in between page refreshes
            let token = String(user['access_token']).replace(/['"]+/g, '');
            console.log(token);
            // token = token.substring(1, token.length() - 1);
            this.setStorage(token);
        }));
    }

    setStorage(user: string) {
        localStorage.setItem('id_token', user);
    }
    getStorage() {
       return localStorage.getItem('id_token');
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
    GetuserID() {
        console.log(this.getStorage());
        const autorization = {Authorization: 'JWT ' + this.getStorage()};
        return this.http.get(environment.adress + '/protected', { headers: autorization }).pipe(map( user => {
            console.log(user);
        }));
    }
}

