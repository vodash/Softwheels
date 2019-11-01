import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class AuthService {

    constructor(private http: HttpClient) {
    }

    login(email: string, password: string ) {
        return this.http.post('10.0.96.154:8000', {email, password});
        // this is just the HTTP call,
        // we still need to handle the reception of the token
    }
}
