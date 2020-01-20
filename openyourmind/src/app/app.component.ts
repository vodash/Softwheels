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
    secretary;
    constructor(private _router: Router, private authService: AuthService) { }

    ngOnInit() {
        this.authService.getUserID()
            .subscribe((value) => {
                this.admin = true;  //change with 'value' after testing is done
                this.secretary = false;
                console.log(this.admin);
            });
    }
}

