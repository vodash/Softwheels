import {Component, HostBinding, Input, Output} from '@angular/core';
import {trigger, state, style, transition, animate} from '@angular/animations';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
    animations: [
        trigger('slideInOut', [
            state('out', style({
                transform: 'translate3d(0, 0, 0)'
            })),
            state('in', style({
                transform: 'translate3d(-100%, 0, 0)'
            })),
            transition('in => out', animate('400ms ease-in-out')),
            transition('out => in', animate('400ms ease-in-out'))
        ]),
    ]
})
export class AppComponent {
    title = 'Open your mind';

    menuState = 'in';
    @HostBinding('class.change') someField = false;

    onHide(val: string) {
        this.menuState = val;
    }

    ngInit() {
        this.someField = true; // set class `someClass` on `<body>`
    }

    toggleMenu() {
        this.menuState = (this.menuState === 'out') ? 'in' : 'out';
        this.someField = (this.menuState === 'out') ? true : false;
    }

    forceCloseMenu() {
        this.menuState = 'in';
        this.someField = false;
    }
}
