import { Component, OnInit } from '@angular/core';
import {AuthService} from "../../authentication/authService";

@Component({
  selector: 'app-therapists',
  templateUrl: './therapists.component.html',
  styleUrls: ['./therapists.component.css']
})
export class TherapistsComponent implements OnInit {

    therapists = ['Therapist 1','Therapist 2','Therapist 3','Therapist 4','Therapist 5','Therapist 6'];
    constructor(private authService: AuthService) { }

    ngOnInit() {
        //This should get all therapist account that belong to the company, posted all patients code for reference
        // let i = 0;
        // this.authService.getPatients()
        //     .subscribe((value) => {
        //         for (const patients in value) {
        //             this.patients.push(value[i][1]);
        //             i++;
        //         }
        //     });

    }

}
