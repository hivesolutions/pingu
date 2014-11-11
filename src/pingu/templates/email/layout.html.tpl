<!DOCTYPE html>
<html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        <center>
            <table width="560" cellpadding="0" cellspacing="0" border="0"
                   style="background: #fdfdfd; padding: 24px 32px 24px 32px">
                <tr>
                    <td height="30"></td>
                </tr>
                <tr>
                    <td align="center">
                        <a href="http://pinguapp.com">
                            <img src="http://pinguapp.com/static/images/logo-email.png" height="30" width="100" alt=""
                                 style="border: none" />
                        </a>
                    </td>
                </tr>
                <tr>
                    <td height="60"></td>
                </tr>
                <tr>
                    <td align="center">
                        <font face="Trebuchet MS, Arial, Helvetica, sans-serif" size="5" color="#333333"
                              style="font-size: 20px; letter-spacing: 0.05em">
                            <strong>{% block title %}{% endblock %}</strong>
                        </font>
                    </td>
                </tr>
                <tr>
                    <td height="20"></td>
                </tr>
                <tr>
                    <td>
                        <font face="Trebuchet MS, Arial, Helvetica, sans-serif" size="2" color="#5b5b5b"
                              style="font-size: 14px; line-height: 24px">
                            {% block content %}{% endblock %}
                        </font>
                    </td>
                </tr>
                <tr>
                    <td height="100"></td>
                </tr>
                <tr>
                    <td align="center">
                        <table width="140" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                                <td height="6"></td>
                            </tr>
                            <tr>
                                <td align="center">
                                    <a href="http://pinguapp.com">
                                        <img src="http://pinguapp.com/static/images/logo-footer-email.png" height="25" width="25" alt=""
                                             style="border: none" />
                                    </a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td height="30"></td>
                </tr>
            </table>
        </center>
    </body>
</html>
