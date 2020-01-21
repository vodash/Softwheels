import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from './authentication/authService';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
    title = 'Open your mind';
    admin;
    secretary;
    constructor(private _router: Router, private authService: AuthService) { }

    ngOnInit() {
        this.authService.getUserID()
            .subscribe((value) => {
                this.admin = value; //change with 'value' after testing is done
                console.log(this.admin);
            });
            this.authService.getSecretary()
            .subscribe((value) => {
                //change with 'value' after testing is done
                this.secretary = value;
                console.log(this.secretary);
            });
    }
}

