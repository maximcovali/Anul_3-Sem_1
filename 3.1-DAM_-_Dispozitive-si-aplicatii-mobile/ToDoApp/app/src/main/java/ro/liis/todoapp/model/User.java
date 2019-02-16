package ro.liis.todoapp.model;

import java.io.Serializable;

public class User implements Serializable{
    private String name;
    private String password;

    public User(String name, String password) {
        this.setName(name);
        this.password = password;
    }

    public int getPassword() {
        return password.hashCode();
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        if(name != null && name.length() > 4) {
            this.name = name;
        }
    }
}
