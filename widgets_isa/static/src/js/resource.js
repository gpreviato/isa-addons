
var varurl = "www.cambiami.com";


openerp.widgets_isa = function (openerp)
{  
    openerp.web.form.widgets.add('test', 'openerp.widgets_isa.Mywidget');
    openerp.widgets_isa.Mywidget = openerp.web.form.FieldChar.extend(
        {
        template : "test",
        init: function (view, code) {
            this._super(view, code);
        },
        set_value: function (value) {
            if (!value) {
                return;
            }
            var s = /(\w+):(.+)/.exec(value);
            if (!s) {
                varurl = "http://" + value;
            } else {
                varurl =  value;
            }
        }
    });
    openerp.web.form.widgets.add('isaurl', 'openerp.widgets_isa.IsaUrlwidget');
    openerp.widgets_isa.IsaUrlwidget = openerp.web.page.FieldURIReadonly.extend({
        set_value: function (value) {
            if (!value) {
                this.$element.find('a').text('').attr('href', '#');
                return;
            }
            var s = /(\w+):(.+)/.exec(value);
            if (!s) {
                value = "http://" + value;
            }
            this.$element.find('a').attr('href', value).attr('target','new').text(value);
        }
   });
}
