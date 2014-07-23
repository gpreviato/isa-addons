## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            .overflow_ellipsis {
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }

            ${css}

.style-r2 {
    background-color: #efefef;
}
        </style>
    </head>
    <body>

        <%!
        def amount(text):
            return text.replace('-', '&#8209;')  # replace by a non-breaking hyphen (it will not word-wrap between hyphen and numbers)
        %>

        <%setLang(user.lang)%>

        <%
        initial_balance_text = {'initial_balance': _('Computed'), 'opening_balance': _('Opening Entries'), False: _('No')}
        %>
		%for inv in objects :
		    <% get_wizard_params(data["form"]["date_maturity_from"],data["form"]["date_maturity_to"],data["form"]["partner_wizard"]) %>
		%endfor

        <div class="act_as_table data_table">
            <div class="act_as_row labels">
                <div class="act_as_cell">${_('Da Data')}</div>
                <div class="act_as_cell">${_('A Data')}</div>
                <div class="act_as_cell">${_('Filtro Partner')}</div>
                <div class="act_as_cell"></div>
                <div class="act_as_cell"></div>
            </div>
            <div class="act_as_row">
                <div class="act_as_cell">${_('Da:')} ${formatLang(data["form"]["date_maturity_from"] or '', date=True)}</div>
                <div class="act_as_cell">${_('A:')} ${formatLang(data["form"]["date_maturity_to"] or '', date=True)}</div>
                <div class="act_as_cell">${ data["form"]["partner_wizard"][1] }</div>
                <div class="act_as_cell"><br></div>
                <div class="act_as_cell"><br></div>
            </div>
        </div>

                    <div class="act_as_table list_table" style="margin-top: 10px;">
                        
                        <div class="act_as_caption account_title">
                            <br>
                        </div>
        
                        <div class="act_as_thead">
                            <div class="act_as_row labels">
                                <div class="act_as_cell first_column" style="width: 50px;">${_('FATTURA')}</div>
                                <div class="act_as_cell" style="width: 70px;">${_('DATA FATTURA')}</div>
                                <div class="act_as_cell" style="width: 70px;">${_('DOCUMENTO DI ORIGINE')}</div>
                                <div class="act_as_cell" style="width: 70px;">${_('PARTNER')}</div>
                                <div class="act_as_cell" style="width: 60px;">${_('REF. PARTNER')}</div>
                                <div class="act_as_cell" style="width: 250px;">${_('TERMINI DI PAGAMENTO')}</div>
                                <div class="act_as_cell" style="width: 60px;">${_("CONTABILITA'")}</div>
                                <div class="act_as_cell amount" style="width: 80px;">${_('DARE')}</div>
                                <div class="act_as_cell amount" style="width: 80px;">${_('AVERE')}</div>
                                <div class="act_as_cell" style="width: 80px;">${_('DATA SCADENZA')}</div>
                                <div class="act_as_cell" style="width: 80px;">${_('MOVIMENTO CONTABILE')}</div>
                                <div class="act_as_cell" style="width: 80px;">${_('RICONCILIA')}</div>
                                <div class="act_as_cell" style="width: 80px;">${_('RICONCILIA PARZIALE')}</div>
                            </div>
                        </div>

                        <div class="act_as_tbody">

                          %for line in get_move_line():
                            <div class="act_as_row lines">
                                <div class="act_as_cell first_column">${line.stored_invoice_id.number or ''}</div>
                                <div class="act_as_cell">${line.invoice_date and (formatLang(line.invoice_date, date=True)) or ''}</div>
                                <div class="act_as_cell">${line.invoice_origin or ''}</div>
                                <div class="act_as_cell">${line.partner_id.name or ''}</div>
                                <div class="act_as_cell">${line.partner_id.ref or ''}</div>
                                <div class="act_as_cell">
							        %if line.payment_term_id and line.payment_term_id.name:
							            ${line.payment_term_id.name}
							        %else:
							            ${''}
							        %endif
						        </div>
                                <div class="act_as_cell">${line.account_id.code} - ${line.account_id.name}</div>
                                <div class="act_as_cell amount">${line.debit}</div>
                                <div class="act_as_cell amount">${line.credit}</div>
                                <div class="act_as_cell">${line.date_maturity and (formatLang(line.date_maturity, date=True)) or ''}</div>
                                <div class="act_as_cell">${line.move_id.name or ''}</div>
                                <div class="act_as_cell">${line.reconcile_id.name or ''}</div>
                                <div class="act_as_cell" style="padding-right: 1px;">${get_reconcile_name(line.reconcile_partial_id.id)}</div>
                            </div>

					      %endfor

                    </div>
                </div>
</body>
</html>
