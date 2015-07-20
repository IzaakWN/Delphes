//==============================================================================================
TLorentzVector ExoDiBosonAnalysis::getp4NuMethod2( void ){

   double E_l  = leptonCand_[0].p4.E();
   double m_l  = leptonCand_[0].p4.M();
   double px_l = leptonCand_[0].p4.Px();
   double py_l = leptonCand_[0].p4.Py();
   double pz_l = leptonCand_[0].p4.Pz();
      
   double px_v = METCand_[0].p4.Px();
   double py_v = METCand_[0].p4.Py();
      
   double m_W = 80.4;
   
   double a = m_W*m_W - m_l*m_l + 2*px_l*px_v + 2*py_l*py_v;
   double A = 4*(E_l*E_l - pz_l*pz_l);
   double B = (-4)*a*pz_l;
   double C = 4*E_l*E_l*(px_v*px_v + py_v*py_v) - a*a;
   double Delta = B*B - 4*A*C;
   
   double pz_v_1 = -9999;
   double pz_v_2 = -9999;
   double pz_v   = -9999;
      
   if( Delta > 0 ){
      pz_v_1 = ( -B + TMath::Sqrt(Delta) )/( 2*A );
      pz_v_2 = ( -B - TMath::Sqrt(Delta) )/( 2*A ); 
      if( fabs(pz_v_1) <= fabs(pz_v_2) ) pz_v = pz_v_1;
      else pz_v = pz_v_2;2
   }
   else if ( Delta <= 0 )
      pz_v = -B/(2*A);

   TLorentzVector v; v.SetPxPyPzE(px_v,py_v,pz_v,fabs(TMath::Sqrt(pz_v*pz_v + py_v*py_v + px_v*px_v)));
//   v.SetPz(pz_v);
//   v.SetPx(px_v);
//   v.SetPy(py_v);
//   v.SetE(fabs(TMath::Sqrt(pz_v*pz_v + py_v*py_v + px_v*px_v)));  
   
   return v;
      
}

//==============================================================================================
void ExoDiBosonAnalysis::findExoCandidate( void ){

   TLorentzVector p4nu = getp4Nu();      
   MWW = (p4nu + leptonCand_[0].p4 + fatJetCand_[jetIndex_].p4).M();
   WMass = (p4nu + leptonCand_[0].p4).M();
   
   TLorentzVector p4nu2 = getp4NuMethod2();

   MWWmethod2 = (p4nu2 + leptonCand_[0].p4 + fatJetCand_[0].p4).M();  
   WMassMethod2 = (p4nu2 + leptonCand_[0].p4).M();  

   return;
            
}

