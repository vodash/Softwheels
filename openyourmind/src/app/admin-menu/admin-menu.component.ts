import {Component, EventEmitter, Output} from '@angular/core';
import {AuthService} from '../authentication/authService';
import {Router} from '@angular/router';

@Component({
  selector: 'app-admin-menu',
  templateUrl: './admin-menu.component.html',
  styleUrls: ['./admin-menu.component.css']
})
export class AdminMenuComponent {

    constructor(
        private authService: AuthService,
        private router: Router
    ) { }

    @Output() closeEvent: EventEmitter<string> = new EventEmitter();

    logout() {
        this.authService.logout();
        this.router.navigateByUrl('/');
    }
}
