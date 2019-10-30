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
            this.setStorage(token);
        }));
    }

    setStorage(user: string) {
        localStorage.setItem('id_token', user);
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
    getStorage() {
        return localStorage.getItem('id_token');
    }
    GetuserID() {
        console.log(this.getStorage());
        const autorization = {Authorization: 'JWT ' + this.getStorage()};
        return this.http.get(environment.adress + '/protected', { headers: autorization }).pipe(map( user => {
            console.log(user);
        }));
    }
    GetdataonID() {
        console.log(this.getStorage());
        const autorization = {Authorization: 'JWT ' + this.getStorage()};
        return this.http.get(environment.adress + '/fake', { headers: autorization }).pipe(map( data => {
            console.log(data);
            console.log(data['hoi'][0]["name"]);
        }));
    }

}

