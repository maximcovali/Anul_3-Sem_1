package ro.liis.todoapp;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.ArrayList;

import ro.liis.todoapp.model.User;

public class RegisterActivity extends AppCompatActivity {
    public final static String usersFile = "users.bin";
    private EditText usernameEditText = null;
    private EditText passwordEditText = null;
    private EditText repeatPasswordEditText = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        usernameEditText = findViewById(R.id.registerUserEditText);
        passwordEditText = findViewById(R.id.registerPasswordEditText);
        repeatPasswordEditText = findViewById(R.id.repeatPasswordEditText);
    }

    public void RegisterUser(View view) {
        if(Validate()) {
            String username = usernameEditText.getText().toString();
            String password = passwordEditText.getText().toString();
            User user = new User(username, password);
            try {
                FileOutputStream fileOutputStream =
                        openFileOutput(usersFile, MODE_PRIVATE);
                if(MainActivity.userList == null) {
                    MainActivity.userList = new ArrayList<>();
                }
                MainActivity.userList.add(user);
                ObjectOutputStream stream = new ObjectOutputStream(fileOutputStream);
                stream.writeObject(MainActivity.userList);
                stream.close();
                fileOutputStream.close();
                finish();
            } catch (IOException e) {
                Toast.makeText(getApplicationContext(), "Something went wrong",
                        Toast.LENGTH_LONG).show();
                e.printStackTrace();
            }
        }
    }

    private boolean Validate() {
        boolean incorrectUser =
                usernameEditText.getText().toString().trim().length() <= 4;
        boolean incorrectPassword =
                passwordEditText.getText().toString().trim().length() <= 4;
        if(incorrectUser || incorrectPassword) {
            Toast.makeText(getApplicationContext(), R.string.incorrect_login,
                    Toast.LENGTH_LONG).show();
            return false;
        }
        boolean passswordsMatch = passwordEditText.getText().toString().
                equals(repeatPasswordEditText.getText().toString());
        if(!passswordsMatch) {
            Toast.makeText(getApplicationContext(), "Passwords don't match!",
                    Toast.LENGTH_LONG).show();
            return false;
        }
        return true;
    }
}
