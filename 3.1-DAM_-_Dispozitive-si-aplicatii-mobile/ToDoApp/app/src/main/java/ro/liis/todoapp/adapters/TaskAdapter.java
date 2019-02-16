package ro.liis.todoapp.adapters;

import android.content.Context;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.List;

import ro.liis.todoapp.R;
import ro.liis.todoapp.model.Task;

public class TaskAdapter extends ArrayAdapter<Task>{

    public TaskAdapter(@NonNull Context context, int resource, @NonNull List<Task> objects) {
        super(context, resource, objects);
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        if(convertView == null) {
            LayoutInflater inflater =
                    LayoutInflater.from(getContext());
            convertView =
                    inflater.inflate(R.layout.task_item, null);

        }
        TextView titleTextView =
                convertView.findViewById(R.id.titleTextView);
        TextView descTextView =
                convertView.findViewById(R.id.descriptionTextView);
        TextView dueDateTextView =
                convertView.findViewById(R.id.dueDateTextView);
        TextView priorityTextView =
                convertView.findViewById(R.id.priorityTextView);
        Task t = getItem(position);
        titleTextView.setText(t.title);
        descTextView.setText(t.description);
        priorityTextView.setText("Priority: " + (t.priority + 1)+ "/4");
        SimpleDateFormat f =
                new SimpleDateFormat("dd.MM.yyyy");
        if(t.dueDate != null) {
            dueDateTextView.setText(f.format(t.dueDate));
        }
        else {
            dueDateTextView.setText("no due date");
        }

        return convertView;
    }
}
