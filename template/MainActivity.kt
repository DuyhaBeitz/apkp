package {{pkgname}}

import android.app.Activity
import android.os.Bundle
import android.view.*
import android.widget.*
import android.graphics.*
import android.util.*
import android.net.*

class MainActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main)
    }
}