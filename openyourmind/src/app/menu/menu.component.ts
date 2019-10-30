import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {AuthService} from '../authentication/authService';
import {Router} from "@angular/router";

@Component({
    selector: 'app-menu',
    templateUrl: './menu.component.html',
    styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {

    constructor(
        private authService: AuthService,
        private router: Router
    ){ }

    @Output() closeEvent: EventEmitter<string> = new EventEmitter();

    logout() {
        this.authService.logout();
        this.router.navigateByUrl('/');
    }

    ngOnInit() {
    }

}
