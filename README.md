

CREATE TABLE projects (
   id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
   titre TEXT NOT NULL,
   description TEXT NOT NULL,
   type_financement TEXT NOT NULL,
   montant_objectif NUMERIC NOT NULL,
   montant_minimum NUMERIC,
   montant_collecte NUMERIC DEFAULT 0.0,
   montant_maximum NUMERIC,
   date_lancement DATE NOT NULL,
   date_fin DATE NOT NULL,
   duree_collecte INTEGER NOT NULL,
   statut TEXT DEFAULT 'reçu',
   secteur TEXT NOT NULL,
   localisation TEXT NOT NULL,
   tags_impact TEXT[],
   medias TEXT[],
   owner_id UUID REFERENCES auth.users(id),
   coach_id UUID,
   comite_statut TEXT DEFAULT 'en attente',
   created_at TIMESTAMPTZ DEFAULT now()
);