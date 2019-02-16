package ro.liis.todoapp.model;

import java.io.Serializable;
import java.util.Date;

public class Task implements Serializable {
    public String title;
    public String description;
    public Date dueDate;
    public short priority;
}
