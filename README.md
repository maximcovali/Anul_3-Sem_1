# anul_3-sem_1
## DAM
### Toast -> cum sa afisezi un mesaj dintr-un string din Resources

```xml
/*Resources Folder -> strings*/
<string name="button">My Button Name</string>
```

```java
Toast.makeText(MainActivity.this, R.string.button, Toast.LENGTH_SHORT).show();
```
