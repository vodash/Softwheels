import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {Router} from '@angular/router';
import {AuthService} from '../authentication/authService';
import {printLine} from "tslint/lib/verify/lines";


@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css']
})
export class LoginComponent  {
//    form = FormGroup
    form = new FormGroup({
        firstName: new FormControl(''),
        lastName: new FormControl(''),});

    constructor(private fb: FormBuilder,
                private authService: AuthService,
                private router: Router) {
    }

    login() {
        console.log('test')
        const val = this.form.value;
        console.log(val)
        if (val.username && val.password) {
            console.log('test')
            this.authService.login(val.username, val.password)
                .subscribe(
                    () => {
                        console.log("User is logged in");
                        this.router.navigateByUrl('/');
                    }
                );
            console.log('test')
        }
    }
}
