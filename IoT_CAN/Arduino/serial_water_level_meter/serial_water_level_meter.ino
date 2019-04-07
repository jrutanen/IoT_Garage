int data = 0;
int calculate_water_depth(int data);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Read input from A0
  data = analogRead(A0);
  //Water depth, program reports 0, 1, 2, 3 and 4 cm
  int water_depth = calculate_water_depth(data);
  Serial.println(String(water_depth));
  //Read value every 30 seconds
  delay(30000);
  Serial.flush();
}

int calculate_water_depth(int data)
{
  int depth = 0;
  if (data > 562)
  {
      depth = 4;
  }
  else if (data > 542)
  {
    depth = 3;
  }
  else if (data > 400)
  {
    depth = 2;
  }
  else if (data > 200)
  {
    depth = 1;
  }
  return depth;
}
