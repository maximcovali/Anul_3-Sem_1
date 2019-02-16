package ro.liis.todoapp;

import android.Manifest;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Vector;

import ro.liis.todoapp.model.Task;
import ro.liis.todoapp.model.User;

public class MenuActivity extends AppCompatActivity {
    public static final String tasksFile = "tasks.bin";
    public static User currentUser = null;
    private HashMap<String, ArrayList<Task>> taskHashMap =
            new HashMap<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);

        try {
            FileInputStream fileInputStream =
                    openFileInput(tasksFile);
            ObjectInputStream inputStream =
                    new ObjectInputStream(fileInputStream);
            taskHashMap =
                    (HashMap<String, ArrayList<Task>>)inputStream.readObject();
            inputStream.close();
            fileInputStream.close();
        }
        catch(Exception e) {
            e.printStackTrace();
        }
        if(taskHashMap == null) {
            taskHashMap = new HashMap<>();
        }
    }

    @Override
    protected void onStop() {
        super.onStop();
        try {
            File file = new File(tasksFile);
            if(taskHashMap != null && taskHashMap.size() > 0) {
                if(file.exists()) {
                    file.delete();
                }
                FileOutputStream fileOutputStream =
                        openFileOutput(tasksFile, MODE_PRIVATE);
                ObjectOutputStream stream =
                        new ObjectOutputStream(fileOutputStream);
                stream.writeObject(taskHashMap);
                stream.close();
                fileOutputStream.close();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void goToProfile(View view){
        Intent intent =
                new Intent(MenuActivity.this,
                        ProfileActivity.class);
        intent.putExtra("userName", currentUser.getName());
        startActivity(intent);
    }

    public void goToAddTask(View view) {
        Intent intent = new Intent(MenuActivity.this, AddTaskActivity.class);
        startActivityForResult(intent, 100);
    }

    public void goToTaskList(View view) {
        Intent intent = new Intent(MenuActivity.this,
                TaskListActivity.class);
        intent.putExtra("list", taskHashMap.get(currentUser.getName()));
        startActivity(intent);
    }

    public void Logout(View view) {
        currentUser =null;
        finish();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if(requestCode == 100 && resultCode == RESULT_OK) {
            Task t = (Task)data.getSerializableExtra("task");
            ArrayList<Task> array = taskHashMap.get(currentUser.getName());
            if(array == null) {
                taskHashMap.put(currentUser.getName(), new ArrayList<Task>());
            }
            taskHashMap.get(currentUser.getName()).add(t);
        }
    }
}
