import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {AuthService} from '../authentication/authService';


@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent  {

    form = new FormGroup({
        username: new FormControl(''),
        password: new FormControl(''),});

    constructor(private fb: FormBuilder,
                private authService: AuthService,
                private router: Router) {
    }

    login() {
        const val = this.form.value;
        console.log(val)
        if (val.username && val.password) {
            this.authService.login(val.username, val.password)
                .subscribe(
                    () => {
                        console.log("User is logged in");
                         this.router.navigateByUrl('/profile');

                    }
                );
        }
    }
}
