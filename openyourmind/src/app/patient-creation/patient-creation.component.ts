import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup} from "@angular/forms";
import {AuthService} from "../authentication/authService";
import {Router} from "@angular/router";

@Component({
  selector: 'app-patient-creation',
  templateUrl: './patient-creation.component.html',
  styleUrls: ['./patient-creation.component.css']
})
export class PatientCreationComponent {

    form = new FormGroup({
        voornaam: new FormControl(''),
        achternaam: new FormControl(''),
        geboortedatum: new FormControl(''),
        geslacht: new FormControl(''),
        bsn: new FormControl(''),
        wachtwoord: new FormControl(''),
        email: new FormControl(''),
    });

    constructor(private fb: FormBuilder,
                private authService: AuthService, public reRouter: Router
               ) {
    }

    createPatient() {
        const val = this.form.value;
        console.log(val)
        if (val.voornaam && val.achternaam && val.geboortedatum && val.geslacht && val.bsn && val.email) {
            this.authService.createPatient
                (val.voornaam, val.achternaam, val.geboortedatum, val.geslacht, val.bsn, val.wachtwoord, val.email)
                    .subscribe(
                        () => {
                            console.log("patient created?");
                            alert('Patient has been created.');
                            this.reRouter.navigate(['/']);

                        }
                    );
        }
    }
}
