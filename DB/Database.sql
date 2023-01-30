-- Database 

create table if not exists tb_collectionneur(
    user_id serial,
    user_name varchar not null unique,
    user_mail varchar not null unique,
    user_password varchar not  null
);
--ALTER TABLE tb_collectionneur 
--ADD CONSTRAINT pk_user PRIMARY KEY (user_id);

create table if not exists TB_INVENTORY(
    user_id varchar not null unique,
    card_id varchar not null unique,
    card_name varchar not null,
    card_amount integer default 1
);
--ALTER TABLE TB_INVENTORY
--ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES tb_collectionneur (user_id), 
--ADD CONSTRAINT pk_inventory PRIMARY KEY (user_id, card_id);

create table if not exists tb_card_value(
    card_id varchar,
    card_value double precision,
    value_date timestamp
);
--ALTER TABLE tb_card_value 
--ADD CONSTRAINT fk_card_id FOREIGN KEY (card_id) REFERENCES tb_inventory (card_id),
--ADD CONSTRAINT pk_card PRIMARY KEY (card_id, value_date);

/*
create table if not exists tb_card_image(
    card_id varchar,
    image_address varchar
)
ALTER TABLE tb_card_image
ADD CONSTRAINT fk_image_card_id FOREIGN KEY (card_id) REFERENCES tb_card_image (card_id)
ADD CONSTRAINT pk_card_image PRIMARY KEY (card_id)
*/

-- insert new user
/*
insert into tb_collectionneur
('1','Adrien','adrien@mail.fr',md5('motdepasse')),
('1','Adrien','adrien@mail.fr',md5('motdepasse')),
('1','Adrien','adrien@mail.fr',md5('motdepasse')),
('1','Adrien','adrien@mail.fr',md5('motdepasse'));
*/

-- insert new card into inventory
/*
insert into tb_user_inventory values
('1','103524','Gate Guardian',1)
on conflict (user_id, card_id) do update
set card_amount = tb_user_inventory.card_amount + 1
*/

-- Assign value to a card at a specific time
/*
insert into tb_card values
('103524', 13.41, now())
*/

-- querry to select cardscwith most recent value based on user
/*
select 
    A.card_id,
    A.card_name,
    A.card_amount,
    B.card_value as unique_value,
    (B.card_value * A.card_amount) as total_value,
    B.value_date
from tb_user_inventory A
left join tb_card_value B on A.card_id = B.card_id
WHERE B.value_date= (SELECT MAX(value_date) FROM tb_card_value WHERE card_id=A.card_id)
*/




