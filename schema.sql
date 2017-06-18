drop table if exists channels;
drop table if exists videos;
create table channels (
	id text primary key,
	name text not null, 
	image text not null,
	description text not null
);
create table videos (
	id text primary key,
	channelid text not null,
	name text not null,
	image text not null,
	description text not null
);