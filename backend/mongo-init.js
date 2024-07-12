//this file is to insert an admin user to the users collection

db = db.getSiblingDB('appointment_manager');

db.createUser({
  user: "admin",
  pwd: "admin",
  roles: [
    {
      role: "readWrite",
      db: "appointment_manager"
    }
  ]
});

// Insert the admin user into the users collection if not present
if (!db.users.findOne({ phone: "admin" })) {
  db.users.insert({
    phone: "admin",
    full_name: "admin admin",
    email: "admin@email.com",
    hashed_password: "$2b$12$fhADMwigzjfkEja34vtCJ.2yrdMXUoXMoHCXNr6gmSMWUfEHjBuI2",  // The password is admin
    disabled: false,
    role: "admin",
  });
}
