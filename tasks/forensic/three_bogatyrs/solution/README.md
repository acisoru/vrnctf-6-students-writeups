# Решение

Перед нами есть три файла: logs.txt - логи, похожие на логи какого-нибудь nginx, MyClass.class - сбилженный java код,
python-obf.py - обфусцированный код питона.
Декомпилируем MyClass.class - видим secretMessage, переводим из HEX в ASCII, получаем одну из частей флага `1_l0v3_`
Шаримся по псевдологам nginx, находим запрос на /admin?redirect=<some_base64>&flag=true, переводим base64, получаем обсуфцированный javascript
```
eval(function(p,a,c,k,e,d){e=function(c){return c.toString(36)};if(!''.replace(/^/,String)){while(c--){d[c.toString(a)]=k[c]||c.toString(a)}k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1};while(c--){if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c])}}return p}('g f(){d=c.9("a").b;3="e p n o m l h";1=i.2(" ");0=3.2(" ");5(1.6!=0.6){7("j");4}5(8(1)==8(0)){7("k");4}}',26,26,'answer_list|input_list|split|password|return|if|length|alert|parseInt|getElementById|input|value|document|some_input|118|checkSecret|function|123|userInput|Pupupu|Yeeeee|102|116|110|99|114'.split('|'),0,{}))
```

Деобфусцируем
```
function checkSecret() {
    some_input = document.getElementById("input").value;
    password = "118 114 110 99 116 102 123";
    input_list = userInput.split(" ");
    answer_list = password.split(" ");
    if (input_list.length != answer_list.length) {
        alert("Pupupu");
        return;
    }
    if (parseInt(input_list) == parseInt(answer_list)) {
        alert("Yeeeee");
        return;
    }
}
```

переводим в ASCII `vrnctf{`

Наконец, видим, что питон обфусцирован Anubisом, находим его на гитхабе https://github.com/0sir1ss/Anubis, деобфусцируем код, находим строчку с флагом, вытаскиваем бинарный код, переводим в ASCII `c4bb463}`

Собираем флаг `vrnctf{1_l0v3_c4bb463}`