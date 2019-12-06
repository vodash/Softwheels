import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map} from 'rxjs/operators';
import {environment} from '../../htpp-conf';
import {Router} from '@angular/router';
import {Observable} from "rxjs";
import {ChartData} from "../models/chartdata.model";

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    constructor(private http: HttpClient, public reRouter: Router) {}

    login(username: string, password: string ) {
        console.log(username, password);
        return this.http.post(environment.adress + '/auth', {username, password}).pipe(map(user => {
            // store user details and jwt token in local storage to keep user logged in between page refreshes
            const token = String(user['access_token']).replace(/['"]+/g, '');
            console.log(token);
            this.setStorage(token);
        }));
    }
    createPatient(voornaam: string, achternaam: string, geboortedatum: string,
                  geslacht: string, bsn: string, wachtwoord: string, email: string ) {
        const autorization = {Authorization: 'JWT ' + this.getStorage()};
        return this.http.post(environment.adress + '/addpatient', {voornaam, achternaam, geboortedatum, geslacht, bsn, wachtwoord, email},
            { headers: autorization }).pipe(map(user => {
            console.log('als het goed is, is er nu een user.');
        }));
    }

    setStorage(user: string) {
        localStorage.setItem('id_token', user);
    }
    logout() {
        localStorage.removeItem('id_token');
    }
    isLoggedIn(): boolean {
        return !!localStorage.getItem('id_token');
    }
    getStorage() {
        return localStorage.getItem('id_token');
    }
    getUserID() {
        console.log(this.getStorage());
        const autorization = {Authorization: 'JWT ' + this.getStorage()};
        return this.http.get(environment.adress + '/isAdmin', { headers: autorization }).pipe(map( user => {
            console.log(user);
        }));
    }
    getDataOnID() {
        console.log(this.getStorage());
        const autorization = {Authorization: 'JWT ' + this.getStorage()};
        return this.http.get<ChartData[]>(environment.adress + '/fake', { headers: autorization }).pipe(
        // map( data => {
        //     console.log(data);
        // })
        );
    }
    getPatientList() {
        const autorization = {Authorization: 'JWT ' + this.getStorage()};
        return this.http.get(environment.adress + '/fake', { headers: autorization }).pipe(
            // map( data => {
            //     console.log(data);
            // })
        );
    }

}

