import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {AuthService} from './authentication/authService';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit{
    title = 'Open your mind';
    admin;
    constructor(private _router: Router, private authService: AuthService) { }

    ngOnInit() {}
    checkAdmin() {
        this.authService.getUserID()
            .subscribe((value) => {
                this.admin = value;
                console.log(this.admin);
            });
    }
}

