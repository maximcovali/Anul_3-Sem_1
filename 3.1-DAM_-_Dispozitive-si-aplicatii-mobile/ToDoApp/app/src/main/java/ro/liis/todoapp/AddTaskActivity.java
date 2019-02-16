package ro.liis.todoapp;

import android.content.Intent;
import android.provider.CalendarContract;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.SeekBar;
import android.widget.Toast;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import ro.liis.todoapp.model.Task;

public class AddTaskActivity extends AppCompatActivity {
    private EditText titleEditText = null;
    private EditText descEditText = null;
    private EditText dueDateEditText = null;
    private SeekBar prioritySeekBar = null;
    private CheckBox addToCalendarCheckBox = null;
    private SimpleDateFormat format =
            new SimpleDateFormat("yyyy-MM-dd");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_task);

        titleEditText = findViewById(R.id.titleEditText);
        descEditText = findViewById(R.id.descriptionEditText);
        dueDateEditText = findViewById(R.id.dueDateEditText);
        prioritySeekBar = findViewById(R.id.prioritySeekBar);
        addToCalendarCheckBox = findViewById(R.id.calendarCheckBox);
    }

    public void AddTask(View view){
        Task t = new Task();
        t.title = titleEditText.getText().toString();
        if(t.title.trim().length() == 0) {
            Toast.makeText(getApplicationContext(), "Enter a title",
                    Toast.LENGTH_LONG).show();
            return;
        }
        t.description = descEditText.getText().toString();
        t.priority = (short)prioritySeekBar.getProgress();
        try {
            t.dueDate = format.parse(dueDateEditText.getText().toString());
        } catch (ParseException e) {
            if(dueDateEditText.getText().toString().length() > 0) {
                Toast.makeText(getApplicationContext(), "Enter a valid date",
                        Toast.LENGTH_LONG).show();
                return;
            }
            e.printStackTrace();
        }

        if(addToCalendarCheckBox.isChecked()) {
            AddTaskToCalendar(view);
        }

        Intent i = new Intent();
        i.putExtra("task", t);
        setResult(RESULT_OK, i);
        finish();
    }

    public void AddTaskToCalendar(View view) {
        Intent intent = new Intent(Intent.ACTION_INSERT,
                CalendarContract.Events.CONTENT_URI);
        Calendar calendar = Calendar.getInstance();
        String dueDate = dueDateEditText.getText().toString();
        try {
            Date date = format.parse(dueDate);
            calendar.setTime(date);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        intent.putExtra(CalendarContract.Events.TITLE, titleEditText.getText().toString());
        intent.putExtra(CalendarContract.EXTRA_EVENT_ALL_DAY, true);
        intent.putExtra(CalendarContract.EXTRA_EVENT_BEGIN_TIME, calendar.getTimeInMillis());
        startActivity(intent);
    }
}
