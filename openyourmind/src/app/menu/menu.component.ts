import { Component, OnInit, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {

  @Output() closeEvent: EventEmitter<string> = new EventEmitter();

  hideMenu() {
    this.closeEvent.emit('in');
  }

  ngOnInit() {
  }

}
