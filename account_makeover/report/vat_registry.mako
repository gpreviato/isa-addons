<html>
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="content-type"/>

  <style type="text/css">

.style-3 {
    color: black; 
    font-size: 36pt; 
    font-family: "Arial"; 
    font-weight: bold; 
    font-style: normal; 
    text-decoration: none; 
    text-align: left; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap
}

.style-4 {
    color: black; 
    font-size: 36pt; 
    font-family: "Arial"; 
    font-weight: bold; 
}

.style-5 {
    color: black; 
    font-size: 16pt; 
    font-family: "Arial"; 
    font-weight: bold; 
    font-style: normal; 
    text-decoration: none; 
    text-align: center; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap; 
    border-top: 2pt solid black; 
    border-left: 2pt solid black; 
    border-bottom: 4pt solid black; 
    border-right: 1pt solid black;
    height: 40pt;
    background-color: #eeeeff;
}

.style-6 {
    color: black; 
    font-size: 10pt; 
    font-family: "Arial"; 
    font-weight: bold; 
    font-style: normal; 
    text-decoration: none; 
    text-align: center; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap; 
    border-top: 1pt solid black; 
    border-left: 1pt solid black; 
    border-bottom: 2pt solid black
}

.style-7 {
    color: black; 
    font-size: 10pt; 
    font-family: "Arial"; 
    font-weight: bold; 
    font-style: normal; 
    text-decoration: none; 
    text-align: center; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap; 
    border-top: 1pt solid black; 
    border-bottom: 2pt solid black; 
    border-right: 1pt solid black
}

.style-9 {
    font-size: 1pt; 
    border-top: 1pt solid black; 
    border-bottom: 1pt solid black
}

.style-10 {
    color: black; 
    padding-right: 5pt; 
    font-size: 18pt; 
    font-family: "Arial"; 
    font-weight: normal; 
    font-style: italic; 
    text-decoration: none; 
    text-align: right; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap; 
    border-top: 1pt solid black; 
    border-bottom: 2pt solid black
}

.style-r1 {
    background-color: #ffffff;
}

.style-r2 {
    background-color: #efefef;
}

.style-11 {
    color: black; 
    padding-right: 5pt; 
    font-size: 18pt; 
    font-family: "Arial"; 
    font-weight: normal; 
    font-style: normal; 
    text-decoration: none; 
    text-align: center; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap; 
    border-left: 1pt solid black; 
    border-bottom: 0pt solid black; 
    border-right: 0pt black;
    height:40px;
    overflow:hidden;
    page-break-inside: avoid;
    o-text-overflow: clip;
    text-overflow: clip;
}

.style-12 {
    color: black; 
    padding-right: 5pt; 
    font-size: 18pt; 
    font-family: "Arial"; 
    font-weight: normal; 
    font-style: normal; 
    text-decoration: none; 
    text-align: center; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap; 
    border-left: 1pt solid black; 
    border-bottom: 0pt solid black; 
    border-right: 1pt solid black;
    height:40px;
    overflow:hidden;
    page-break-inside: avoid;
    o-text-overflow: clip;
    text-overflow: clip;
}

.style-22 {
    color: black; 
    font-size: 18pt; 
    font-family: "Arial"; 
    font-weight: bold; 
    font-style: normal; 
    text-decoration: none; 
    text-align: center; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap; 
    border: 1pt solid black
}

.style-23 {
    color: black; 
    padding-right: 5pt; 
    font-size: 18pt; 
    font-family: "Arial"; 
    font-weight: normal; 
    font-style: normal; 
    text-decoration: none; 
    text-align: right; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap; 
    border: 1pt solid black
}

.style-71 {
    color: black; 
    font-size: 10pt; 
    font-family: "Arial"; 
    font-weight: bold; 
    font-style: normal; 
    text-decoration: none; 
    text-align: center; 
    word-spacing: 0pt; 
    letter-spacing: 0pt; 
    white-space: pre-wrap;
    border-style:groove;
    border-width:2pt 1pt 1pt 1pt;
    border-color:black;
}

  </style>

</head>
<body>
  <% setLang("it_IT") %>
  <%!
          def amount(text):
              return text.replace('-', '&#8209;')  # replace by a non-breaking hyphen (it will not word-wrap between hyphen and numbers)
  %>

<%  set_dates(data['form'],data['context']) %>

<%  t_date_start = get_date_start() %>
<%  t_date_stop  = get_date_stop() %>
<%  t_date_year  = get_date_year() + '-01-01' %>

<%  line = {} %>

<%  count=0 %>
<%  style="style-11" %>

<% is_group = False %>
<% prev_group = False %>

<%  t_protocol_number         = ''  %>
<%  t_protocol_date           = ''  %>
<%  t_cliente                 = ''  %>
<%  t_supplier_invoice_number = ''  %>
<%  t_date_invoice            = ''  %>
<%  t_num_documento           = ''  %>
<%  t_imponibile              = 0.0 %>
<%  t_cod_iva                 = ''  %>
<%  t_imposta                 = 0.0 %>
<%  t_totale                  = 0.0 %>
<%  t_ref_autoinvoice         = None  %>

<%  t_tot_imponibile  = 0.0 %>
<%  t_tot_imposta     = 0.0 %>
<%  t_tot_documento   = 0.0 %>

        <table width="100%" cellpadding="2" cellspacing="0">
          <thead>

            <tr>
              <td colspan="11">
                <span class="style-4">&nbsp</br>&nbsp</span>
              </td>
            </tr>

            <tr>
              <td colspan="11">
                <span class="style-4">${get_registry_name()}</br>dal ${formatLang(t_date_start, date=True) or ''|entity} al ${formatLang(t_date_stop, date=True) or ''|entity}</span>
              </td>
            </tr>

            <tr valign="top" style="height: 40pt">
              <td valign="middle" class="style-5" style="height:40px; width:130px">${_("Protocollo")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:150px">${_("Data Protocollo")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:250px">${_("Cliente")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:160px">${_("Numero Documento")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:150px">${_("Data Documento")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:220px">${_("Riferim.")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:160px">${_("Imponibile")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:150px">${_("Cod. IVA")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:160px">${_("Imposta")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:160px">${_("Totale doc.")}</td>
              <td valign="middle" class="style-5" style="height:40px; width:130px">${_("Riferim. IntraCEE")}</td>
            </tr>
          </thead>
          <tbody>
            <% row_count = 1 %>
            %for line in get_vat_registry_lines(data['form'],data['context']):

                % if count > 0 and not prev_group:
                  <% style = "style-r1" %>
                  <% count = 0  %>
                % elif not prev_group:
                  <% style = "style-r2" %>
                  <% count = 1 %>
                % endif

                % if t_protocol_number == line['protocol_number']:
                  <% is_group = True %>
                % else:
                  <% is_group = False %>
                % endif

                % if not is_group:
                  <% print_totale = formatLang(t_totale, monetary=True, digits=get_digits(dp='Account')) %>
                % else:
                  <% print_totale = '' %>
                % endif

                % if not prev_group:
                  <% print_protocol_number = t_protocol_number %>
                  <% print_protocol_date = t_protocol_date %>
                  <% print_cliente = t_cliente %>
                  <% print_supplier_invoice_number = t_supplier_invoice_number %>
                  <% print_date_invoice = t_date_invoice %>
                  <% print_num_documento = t_num_documento %>
                  <% print_ref_autoinvoice = t_ref_autoinvoice %>
                % else:
                  <% print_protocol_number = '' %>
                  <% print_protocol_date = '' %>
                  <% print_cliente = '' %>
                  <% print_supplier_invoice_number = '' %>
                  <% print_date_invoice = '' %>
                  <% print_num_documento = '' %>
                  <% print_ref_autoinvoice = '' %>
                % endif

                % if t_protocol_number:
                    <tr valign="top" class="${style}">
                      <td valign="middle" class="style-11">${print_protocol_number}</td>
                      <td valign="middle" class="style-11">${print_protocol_date or ''|entity}</td>
                      <td valign="middle" class="style-11">${print_cliente or ''}</td>
                      <td valign="middle" class="style-11">${print_supplier_invoice_number or ''}</td>
                      <td valign="middle" class="style-11">${print_date_invoice or ''|entity}</td>
                      <td valign="middle" class="style-11">${print_num_documento or ''}</td>
                      
                      <td valign="middle" class="style-11" style="text-align: right">${t_imponibile | amount}</td>
                      <td valign="middle" class="style-11">${t_cod_iva}</td>
                      <td valign="middle" class="style-11" style="text-align: right">${t_imposta | amount}</td>
                      <td valign="middle" class="style-11" style="text-align: right">${print_totale | amount}</td>
                      <td valign="middle" class="style-12">${print_ref_autoinvoice or ''}</td>
                    </tr>
                % endif

                <%  t_protocol_number         = line['protocol_number']  %>
                <%  t_protocol_date           = formatLang(line['protocol_date'], date=True)  %>
                <%  t_cliente                 = line['cliente']  %>
                <%  t_supplier_invoice_number = line['supplier_invoice_number']  %>
                <%  t_date_invoice            = formatLang(line['date_invoice'], date=True)  %>
                <%  t_num_documento           = line['num_documento']  %>
                <%  t_imponibile              = formatLang(line['imponibile'], monetary=True, digits=get_digits(dp='Account')) %>
                <%  t_cod_iva                 = line['cod_iva']  %>
                <%  t_imposta                 = formatLang(line['imposta'], monetary=True, digits=get_digits(dp='Account')) %>
                <%  t_totale                  = t_totale + line['imponibile'] + line['imposta'] %>
                % if line['ref_autoinvoice']:
                    <%  t_ref_autoinvoice         = get_ref_autoinvoice(line['ref_autoinvoice'])  %>
                % else:
                    <%  t_ref_autoinvoice         = None  %>
                % endif

                <% prev_group = is_group %>

                % if not prev_group:
                  <% t_totale = line['imponibile'] + line['imposta'] %>
                % endif

                <%  t_tot_imponibile  = t_tot_imponibile + line['imponibile'] %>
                <%  t_tot_imposta     = t_tot_imposta + line['imposta'] %>
                <%  t_tot_documento   = t_tot_imponibile + t_tot_imposta %>

                <% row_count = row_count + 1 %>
                %if row_count > 24:
                  <% row_count = 1 %>
                      </tbody>
                    </table>

                    <table width="100%" cellpadding="2" cellspacing="0" style="page-break-before: always">
                      <thead>
            
                        <tr>
                          <td colspan="11">
                            <span class="style-4">&nbsp</br>&nbsp</span>
                          </td>
                        </tr>
            
                        <tr>
                          <td colspan="11">
                            <span class="style-4">${get_registry_name()}</br>dal ${formatLang(t_date_start, date=True) or ''|entity} al ${formatLang(t_date_stop, date=True) or ''|entity}</span>
                          </td>
                        </tr>
            
                        <tr valign="top" style="height: 40pt">
                          <td valign="middle" class="style-5" style="height:40px; width:130px">${_("Protocollo")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:150px">${_("Data Protocollo")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:250px">${_("Cliente")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:160px">${_("Numero Documento")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:150px">${_("Data Documento")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:220px">${_("Riferim.")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:160px">${_("Imponibile")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:150px">${_("Cod. IVA")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:160px">${_("Imposta")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:160px">${_("Totale doc.")}</td>
                          <td valign="middle" class="style-5" style="height:40px; width:130px">${_("Riferim. IntraCEE")}</td>
                        </tr>
                      </thead>
                      <tbody>
                %endif
    
            %endfor

            % if count > 0:
              <% style = "style-r1" %>
              <% count = 0  %>
            % else:
              <% style = "style-r2" %>
              <% count = 1 %>
            % endif

            % if 'protocol_number' in line and line['protocol_number']:
                <%  t_protocol_number         = line['protocol_number']  %>
                <%  t_protocol_date           = formatLang(line['protocol_date'], date=True)  %>
                <%  t_cliente                 = line['cliente']  %>
                <%  t_supplier_invoice_number = line['supplier_invoice_number']  %>
                <%  t_date_invoice            = formatLang(line['date_invoice'], date=True)  %>
                <%  t_num_documento           = line['num_documento']  %>
                <%  t_imponibile              = formatLang(line['imponibile'], monetary=True, digits=get_digits(dp='Account')) %>
                <%  t_cod_iva                 = line['cod_iva']  %>
                <%  t_imposta                 = formatLang(line['imposta'], monetary=True, digits=get_digits(dp='Account')) %>
                <%  t_totale                  = t_totale + line['imponibile'] + line['imposta'] %>
                % if line['ref_autoinvoice']:
                    <%  t_ref_autoinvoice         = get_ref_autoinvoice(line['ref_autoinvoice'])  %>
                % else:
                    <%  t_ref_autoinvoice         = None  %>
                % endif

                <tr valign="top" class="${style}">
                  <td valign="middle" class="style-11">${t_protocol_number}</td>
                  <td valign="middle" class="style-11">${t_protocol_date or ''|entity}</td>
                  <td valign="middle" class="style-11">${t_cliente or ''}</td>
                  <td valign="middle" class="style-11">${t_supplier_invoice_number or ''}</td>
                  <td valign="middle" class="style-11">${t_date_invoice or ''|entity}</td>
                  <td valign="middle" class="style-11">${t_num_documento or ''}</td>
                  <td valign="middle" class="style-11" style="text-align: right">${t_imponibile | amount}</td>
                  <td valign="middle" class="style-11">${t_cod_iva}</td>
                  <td valign="middle" class="style-11" style="text-align: right">${t_imposta | amount}</td>
                  <td valign="middle" class="style-11" style="text-align: right">${formatLang(t_totale, monetary=True, digits=get_digits(dp='Account')) | amount}</td>
                  <td valign="middle" class="style-12">${t_ref_autoinvoice or ''}</td>
                </tr>
                <%  t_tot_imponibile  = t_tot_imponibile + line['imponibile'] %>
                <%  t_tot_imposta     = t_tot_imposta + line['imposta'] %>
                <%  t_tot_documento   = t_tot_imponibile + t_tot_imposta %>
    
                <tr valign="top" style="height: 20pt">
                  <td valign="middle" class="style-10" colspan="5">${_("TOTALE")}</td>
                  <td valign="middle" class="style-10"></td>
                  <td valign="middle" class="style-10" style="text-align: right">${formatLang(t_tot_imponibile) | amount}</td>
                  <td valign="middle" class="style-10"></td>
                  <td valign="middle" class="style-10" style="text-align: right">${formatLang(t_tot_imposta) | amount}</td>
                  <td valign="middle" class="style-10" style="text-align: right">${formatLang(t_tot_documento) | amount}</td>
                  <td valign="middle" class="style-10"></td>
                </tr>
            % endif
          </tbody>
        </table>
        </br>
        </br>
        </br>

        <%  t_riepilogo_sel_imponibile  = 0.0 %>
        <%  t_riepilogo_sel_imposta     = 0.0 %>
        <%  t_riepilogo_sel_documento   = 0.0 %>
        <%  t_riepilogo_tot_imponibile  = 0.0 %>
        <%  t_riepilogo_tot_imposta     = 0.0 %>
        <%  t_riepilogo_tot_documento   = 0.0 %>
        <table width="100%" cellpadding="0" cellspacing="0" style="page-break-before: always;width: 1500pt">
          <thead>
            <tr>
              <td colspan="11">
                <span class="style-4">&nbsp</br>&nbsp</span>
              </td>
            </tr>

            <tr>
              <td colspan="11">
                <span class="style-4">RIEPILOGO</span>
              </td>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td valign="top">
                <table width="100%" cellpadding="8" cellspacing="0">
                  <tr>
                    <td colspan="5" class="style-22">DAL ${formatLang(t_date_start, date=True) or ''|entity} AL ${formatLang(t_date_stop, date=True) or ''|entity}</td>
                  </tr>
                  <tr>
                    <td valign="middle" class="style-5" style="width:220px">${_("DESCRIZIONE")}</td>
                    <td valign="middle" class="style-5" style="width:220px">${_("COD.IVA")}</td>
                    <td valign="middle" class="style-5" style="width:220px">${_("IMPONIBILE")}</td>
                    <td valign="middle" class="style-5" style="width:220px">${_("IMPOSTA")}</td>
                    <td valign="middle" class="style-5" style="width:220px">${_("TOTALE")}</td>
                  </tr>
                  %for line in get_total_selected(data['form'],data['context']):
                     % if count > 0:
                       <% style = "style-r1" %>
                       <% count = 0  %>
                     % else:
                       <% style = "style-r2" %>
                       <% count = 1 %>
                     % endif
                    <tr class="${style}">
                      <td valign="middle" class="style-11">${line['name']}</td>
                      <td valign="middle" class="style-11">${line['cod_iva']}</td>
                      <td valign="middle" class="style-11" style="text-align: right">${formatLang(line['imponibile']) | amount}</td>
                      <td valign="middle" class="style-11" style="text-align: right">${formatLang(line['imposta']) | amount}</td>
                      <td valign="middle" class="style-12" style="text-align: right">${formatLang(line['tot_riga']) | amount}</td>
                    </tr>
                  <%  t_riepilogo_sel_imponibile  = t_riepilogo_sel_imponibile + line['imponibile'] %>
                  <%  t_riepilogo_sel_imposta     = t_riepilogo_sel_imposta + line['imposta'] %>
                  <%  t_riepilogo_sel_documento   = t_riepilogo_sel_imponibile + t_riepilogo_sel_imposta %>
                  %endfor
                  <tr>
                    <td colspan="2" class="style-10">${_("TOTALE")}</td>
                    <td colspan="1" class="style-10" style="text-align: right">${formatLang(t_riepilogo_sel_imponibile) | amount}</td>
                    <td colspan="1" class="style-10" style="text-align: right">${formatLang(t_riepilogo_sel_imposta) | amount}</td>
                    <td colspan="1" class="style-10" style="text-align: right">${formatLang(t_riepilogo_sel_documento) | amount}</td>
                  </tr>
                </table>
              </td>
              <td valign="top">
                <table width="100%" cellpadding="8" cellspacing="0">
                  <tr>
                    <td colspan="5" class="style-22">DAL ${formatLang(t_date_year, date=True) or ''|entity} AL ${formatLang(t_date_stop, date=True) or ''|entity}</td>
                  </tr>
                  <tr>
                    <td valign="middle" class="style-5" style="width:220px">${_("DESCRIZIONE")}</td>
                    <td valign="middle" class="style-5" style="width:220px">${_("COD.IVA")}</td>
                    <td valign="middle" class="style-5" style="width:220px">${_("IMPONIBILE")}</td>
                    <td valign="middle" class="style-5" style="width:220px">${_("IMPOSTA")}</td>
                    <td valign="middle" class="style-5" style="width:220px">${_("TOTALE")}</td>
                  </tr>
                  %for line in get_total_start_year(data['form'],data['context']):
                     % if count > 0:
                       <% style = "style-r1" %>
                       <% count = 0  %>
                     % else:
                       <% style = "style-r2" %>
                       <% count = 1 %>
                     % endif
                    <tr class="${style}">
                      <td valign="middle" class="style-11">${line['name']}</td>
                      <td valign="middle" class="style-11">${line['cod_iva']}</td>
                      <td valign="middle" class="style-11" style="text-align: right">${formatLang(line['imponibile']) | amount}</td>
                      <td valign="middle" class="style-11" style="text-align: right">${formatLang(line['imposta']) | amount}</td>
                      <td valign="middle" class="style-12" style="text-align: right">${formatLang(line['tot_riga']) | amount}</td>
                    </tr>
                  <%  t_riepilogo_tot_imponibile  = t_riepilogo_tot_imponibile + line['imponibile'] %>
                  <%  t_riepilogo_tot_imposta     = t_riepilogo_tot_imposta + line['imposta'] %>
                  <%  t_riepilogo_tot_documento   = t_riepilogo_tot_imponibile + t_riepilogo_tot_imposta %>
                  %endfor
                  <tr>
                    <td colspan="2" class="style-10">${_("TOTALE")}</td>
                    <td colspan="1" class="style-10" style="text-align: right">${formatLang(t_riepilogo_tot_imponibile) | amount}</td>
                    <td colspan="1" class="style-10" style="text-align: right">${formatLang(t_riepilogo_tot_imposta) | amount}</td>
                    <td colspan="1" class="style-10" style="text-align: right">${formatLang(t_riepilogo_tot_documento) | amount}</td>
                  </tr>
                </table>
              </td>
            </tr>
          </tbody>
        </table>
</body>
</html>
