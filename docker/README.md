## docker part

simple dockerfile with user non root to run the script

base image used is the official slim python image

setuid and setgid permission were removed ( not elegant as any error raised
with the find is escaped, would be better to docker edit and then commit again the image)
