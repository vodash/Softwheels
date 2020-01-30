import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import {AuthService} from '../authentication/authService';
import {Router} from '@angular/router';

@Component({
  selector: 'app-secretary-menu',
  templateUrl: './secretary-menu.component.html',
  styleUrls: ['./secretary-menu.component.css']
})
export class SecretaryMenuComponent {


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
