import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map} from 'rxjs/operators';
import {environment} from '../../htpp-conf';

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    constructor(private http: HttpClient) {
    }

    login(username: string, password: string ) {
        console.log(username, password);
        return this.http.post(environment.adress + '/auth', {username, password}).pipe(map(user => {
            // store user details and jwt token in local storage to keep user logged in between page refreshess
            this.setStorage(user);
        }));
    }

    setStorage(user: object) {
        localStorage.setItem('id_token', JSON.stringify(user) );
    }

    logout() {
        localStorage.removeItem('id_token');
    }
}

