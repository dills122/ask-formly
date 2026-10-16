import { Component } from '@angular/core';
import { FieldWrapper } from '@ngx-formly/core';
@Component({selector: 'section-panel-wrapper', template: '<section><ng-container #fieldComponent></ng-container></section>'})
export class SectionPanelWrapper extends FieldWrapper {}
