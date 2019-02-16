package ro.liis.todoapp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.ListView;

import java.util.ArrayList;
import java.util.Vector;

import ro.liis.todoapp.adapters.TaskAdapter;
import ro.liis.todoapp.model.Task;

public class TaskListActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_task_list);

        Intent intent = getIntent();
        ArrayList<Task> vector =
                (ArrayList<Task>)intent.getSerializableExtra("list");
        if(vector != null) {
            TaskAdapter adapter = new TaskAdapter(getApplicationContext(),
                    R.layout.task_item, vector);
            ListView listView = findViewById(R.id.listView);
            listView.setAdapter(adapter);
        }
    }
}
