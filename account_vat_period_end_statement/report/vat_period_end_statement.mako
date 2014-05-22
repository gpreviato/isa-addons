<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
<% setLang(company.partner_id.lang) %>
% for statement in objects:
<h1>${_("VAT Statement Summary")} </h1>
<h2>${_("Period")}: ${statement.period_id.name|entity}</h2>
<table class="list_table"  width="90%">
    <tr>
        <th></th>
        <th> ${ _('Amount') }</th>
    </tr>
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td><strong>${_("Payable VAT")}</strong></td>
        <td></td>
    </tr>
    %for debit_line in statement.debit_vat_account_line_ids :
        <tr style="page-break-inside: avoid; vertical-align:text-top;">
            <td>${ debit_line.account_id.name|entity }</td>
            <td>${ debit_line.amount|entity }</td>
        </tr>
    %endfor
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td>${_("Total")}</td>
        <td>${ statement.payable_vat_amount|entity }</td>
    </tr>
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td></td>
        <td></td>
    </tr>
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td><strong>${_("Deductible VAT")}</strong></td>
        <td></td>
    </tr>
    %for credit_line in statement.credit_vat_account_line_ids :
        <tr style="page-break-inside: avoid; vertical-align:text-top;">
            <td>${ credit_line.account_id.name|entity }</td>
            <td>${ credit_line.amount|entity }</td>
        </tr>
    %endfor
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td>${_("Total")}</td>
        <td>${ statement.deductible_vat_amount|entity }</td>
    </tr>
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td></td>
        <td></td>
    </tr>
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td>${_("Previous Credits VAT")}</td>
        <td>${ statement.previous_credit_vat_amount|entity }</td>
    </tr>
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td>${_("Previous Debits VAT")}</td>
        <td>${ statement.previous_debit_vat_amount|entity }</td>
    </tr>
    %for generic_line in statement.generic_vat_account_line_ids :
        <tr style="page-break-inside: avoid; vertical-align:text-top;">
            <td>${ generic_line.account_id.name|entity }</td>
            <td>${ generic_line.amount|entity }</td>
        </tr>
    %endfor
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td></td>
        <td></td>
    </tr>
    <tr style="page-break-inside: avoid; vertical-align:text-top;">
        <td><strong>${_("Amount to pay")}</strong></td>
        <td><strong>${ statement.authority_vat_amount|entity }</strong></td>
    </tr>
</table>
%endfor
</body>
</html>
