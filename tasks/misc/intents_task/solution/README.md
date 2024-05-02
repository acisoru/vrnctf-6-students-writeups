# Решение

Разбираем приложение с помощью JADX, там видим что в манифесте экспортировано MainActivity (так как оно является стартовым).

В коде MainActivity видим обработчик интентов. Пытаемся понять, что там происходит, 
шлём am start-activity через adb shell с нужными extras, периодически посматривая adb logcat, если вдруг новый экран не открылся.

Итог:

```shell
adb shell
am start-activity -n ru.vsu.cs.perunvault/.MainActivity -e login ruru -e password 123123
am start-activity -n ru.vsu.cs.perunvault/.MainActivity -e vaultid 1337 -e vaultpass perun
am start-activity -n ru.vsu.cs.perunvault/.MainActivity -e noteid 123456789
```
